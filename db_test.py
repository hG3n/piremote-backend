import database.base
from database.api import Api
from database.models import tables

def set_database_to_default(recreate=True):
  a = None
  if recreate:
    database.base.recreate_database()
    a = Api(bind=database.base.engine)
  else:
    a = Api(bind=database.base.engine)
    a._clear()
  a.close()
  del a
  a = None
  
if __name__ == "__main__":
  a = Api(bind=database.base.engine)
  a.open()
  s = a._db
  
  p = tables.Preset(name='empty nested')
  p.json = """{
  "data": {
      "contents": {
          "scene": {
              "scene_rect": {
                  "height": 1258,
                  "width": 2221,
                  "x": 0,
                  "y": 0
              },
              "tiles": []
          }
      },
      "name": "Nature",
      "position": [
          1074,
          22
      ],
      "size": 2,
      "uuid": "{b712a3cf-ca9b-40b7-9925-39377a758fc4}"
  },
  "type": "TwoD::NestedTile"
  }"""
  s.add(p)
  s.commit()
