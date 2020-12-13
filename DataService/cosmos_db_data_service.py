import utils.context as ctx
from DataService.base_data_service import BaseDataService
import copy
from azure.core._match_conditions import MatchConditions
import flatten_dict


class DataService(BaseDataService):

    _cosmos_rsp_fields = ['_rid', '_self', '_etag', '_attachments', "_ts"]
    _cosmos_obj_field = 'cosmos_props'

    def __init__(self):
        self._db_service = ctx.env["db_settings"]["database_service"]
        self._collection_clients = {}

    def _get_collection_client(self, collection_id):
        result = self._collection_clients.get(collection_id)
        if result is None:
            result = self._db_service.get_container_client(collection_id)
            self._collection_clients[collection_id] = result
        return result

    @staticmethod
    def _build_where_clause(template):

        if template is None:
            result = " FROM c "
        else:
            ar = flatten_dict.flatten(template)

            terms = []
            vals = []
            i = 0

            for k, v in ar.items():
                i += 1
                t = "c." + ".".join(k)
                slot = "@p" + str(i)
                t = t + "=" + slot

                terms.append(copy.copy(t))
                vals.append(dict(name=slot, value=v))

            wc = " and ".join(terms)
            wc = " where " + wc
            return wc, vals

    @staticmethod
    def _process_cosmos_fields(rsp):
        cosmos_fields = {}
        for f in DataService._cosmos_rsp_fields:
            cosmos_fields[f] = copy.copy(rsp.get(f, None))
            del rsp[f]
        rsp[DataService._cosmos_obj_field] = cosmos_fields
        return rsp

    def create(self, collection_id, obj):
        coll = self._get_collection_client(collection_id)
        res = coll.create_item(obj)
        res = DataService._process_cosmos_fields(res)
        return res

    def delete(self, collection_id, obj_id):
        coll = self._get_collection_client(collection_id)
        res = coll.delete_item(obj_id, partition_key=obj_id)
        return res

    def update(self, collection_id, obj_id, obj):
        coll = self._get_collection_client(collection_id)
        res = coll.replace_item(obj_id, obj, etag=obj[DataService._cosmos_obj_field]["_etag"],
                                match_condition=MatchConditions.IfNotModified)
        return res

    def get_by_id(self, collection_id, obj_id):
        coll = self._get_collection_client(collection_id)
        res = coll.read_item(item=obj_id, partition_key=obj_id)
        res = DataService._process_cosmos_fields(res)
        return res

    def query(self, collection_id, template):
        q,p = DataService._build_where_clause(template)
        q = "select * from c " + q

        coll = self._get_collection_client(collection_id)
        res = coll.query_items(query=q, parameters=p, enable_cross_partition_query=True)
        return res








