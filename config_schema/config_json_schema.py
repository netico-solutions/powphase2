valid_schema =\
    {
      "$schema": "http://json-schema.org/draft-04/schema#",
      "type": "object",
      "properties": {
        "main_frequency": {
          "type": "number"
        },

        "temp_calib": {
          "type": "object",
          "properties": {
            "current": {
              "type": "array",
              "items": [
                {
                  "type": "number"
                }
              ]
            },
            "temperature": {
              "type": "array",
              "items": [
                {
                  "type": "number"
                }
              ]
            }
          },
          "required": [
            "current",
            "temperature"
          ]
        },

        "states": {
          "type": "array",
          "items": {
              "type": "object",
              "properties": {
                "angle": {
                  "type": "number"
                },
                "impulse": {
                  "type": "number"
                },
                "index": {
                  "type": "number"
                },
                "time_temp": {
                  "type": "array",
                  "items":
                    {
                      "type": "array",
                      "items": [
                        {
                          "type": "number"
                        },
                        {
                          "type": "array",
                          "items":
                            {
                              "type": "number"
                            },
                          "minItems": 3,
                          "maxItems": 3
                        }],
                      "minItems": 2,
                      "maxItems": 2
                    },
                  "minItems": 2
                },
                "input_signal": {
                  "type": "number"
                },
                "name": {
                  "type": "string"
                }
              },
              "required": [
                "angle",
                "impulse",
                "index",
                "time_temp",
                "input_signal",
                "name"
              ],
            },
          "minItems": 2,
          "maxItems": 2
        }
      },
      "required": [
        "main_frequency",
        "temp_calib",
        "states"
      ]
    }
