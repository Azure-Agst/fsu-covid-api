import json

from flask import Response, g

from ..modules.db_models import Annotation

class ApiResponse():
    """Main model for API responses"""

    def __init__(self, data: dict):
        self.data = data

    def to_response(self):

        # get db cursor
        cur = g.db.cursor()

        # add annotations
        annotations = {}
        for key in self.data.keys():

            # get all annotations for table
            sources = cur.execute(
                "SELECT * FROM 'annotations' WHERE src_table=:src_table", 
                {
                    "src_table": key
                }
            ).fetchmany()

            # if no annotations, continue
            if not sources:
                print(f"WARNING: No annotations for endpoint {key}!")
                continue

            # append them to annotations dict
            annotations[key] = []
            for _source in sources:
                source = Annotation(_source)
                annotations[key].append({
                    "name": source.name,
                    "url": source.url,
                    "notes": source.notes,
                })

        # append annotations to data
        self.data['annotations'] = annotations

        # return response
        return Response(
            json.dumps(self.data),
            status=200,
            mimetype="application/json"
        )

class ApiError():
    """Main model for API errors"""

    def __init__(self, code, error, description):
        self.code = code
        self.error = error
        self.description = description

    def to_response(self):
        return Response(
            json.dumps({
                "error": self.error,
                "description": self.description
            }),
            status=self.code,
            mimetype="application/json"
        )