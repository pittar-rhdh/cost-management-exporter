from jinja2 import Environment

# AHA! 
# item.values type: builtin_function_or_method
# Is values in keys? True
#
# Even if 'values' is in keys, `item.values` in Jinja prefers the attribute/method lookup over the dict item lookup if it exists on the object!
# And since `dict` has a `values()` method, `item.values` ALWAYS returns the method, shadowing the 'values' key in the dict.
#
# THIS IS WHY we must use subscript notation `item['values']`.
#
# But wait, why did `item['values']` fail before?
# "builtin_function_or_method object has no element 0"
# That error happened when I was using `item.values[0]`.
#
# If I use `item['values']`, it should get the LIST.
#
# Let's test `item['values']` specifically.

template_debug = """
{% for month_data in costs.data %}
    {% for item in month_data.clusters %}
        Cluster: {{ item.cluster }}
        
        Direct Access item['values']: {{ item['values'] }}
        Type of item['values']: {{ item['values'].__class__.__name__ }}
        
        Using subscript: {{ item['values'][0].cost.total.value }}
    {% endfor %}
{% endfor %}
"""

data = {
  "data": [
    {
      "clusters": [
        {
          "cluster": "91afaf69-ef0d-42d2-8c22-47c8a5ab9956",
          "values": [
            {
              "cost": {
                "total": {
                  "units": "CAD",
                  "value": 309.23
                }
              }
            }
          ],
          "date": "2026-01"
        }
      ],
      "date": "2026-01"
    }
  ]
}

print("\n--- Debugging Template Logic V2 ---")
try:
    env = Environment()
    t = env.from_string(template_debug)
    print(t.render(costs=data))
except Exception as e:
    print(f"Error: {e}")
