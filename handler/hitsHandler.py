from lambda_decorators import cors_headers, load_json_body, dump_json_body
import traceback, logging, os, uuid, json
from db import hitsDb
from lib import s3Helper

hits_bucket = os.environ.get("HITS_BUCKET")
s3_client = s3Helper.S3Helper(hits_bucket)


@cors_headers
@dump_json_body
@load_json_body
def hits_handler(event, context):
    try:
        logging.info("Received hits")
        body = event['body']

        sid = body.get('sid')
        path = body.get('path')
        hostname = body.get('hostname')
        referrer = body.get('referrer')
        resolution = body.get('resolution')
        timezone = body.get('timezone')
        referrer_param = body.get('referrer_param')
        new_visit = body.get('new_visit')
        new_field = body.get('new_field')

        if not sid or not path or not hostname or not referrer or not resolution or not timezone or not referrer_param \
                or not new_visit:
            return {'statusCode': 400, 'body': {"message": "Missing details"}}
        event_id = str(uuid.uuid1())

        # Storing in Dynamo
        hit_model = hitsDb.create_hit_entry(sid=sid, event_id=event_id, path=path, hostname=hostname, referrer=referrer,
                                            resolution=resolution, timezone=timezone, referrer_param=referrer_param,
                                            new_visit=new_visit)

        # Storing in S3 directly.
        key = "hits_data_lambda/%s.json" % event_id
        s3_client.put_object(key, json.dumps(hit_model.to_dict()), "application/json")

        return {'statusCode': 200, 'body': {"message": "success"}}
    except Exception as e:
        logging.error("Error while handling hits")
        logging.error(traceback.print_exc())
    return {'statusCode': 500, 'body': {"message": "failed"}}

