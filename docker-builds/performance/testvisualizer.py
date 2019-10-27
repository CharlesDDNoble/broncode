import plotly.graph_objects as PGraph

# fig = go.Figure({
#     "data": [{"type": "bar",
#               "x": [1, 2, 3],
#               "y": [1, 3, 2]}],
#     "layout": {"title": {"text": "A Bar Chart"}}
# })

# fig = PGraph.Figure(data=[PGraph.Bar(x=[1, 2, 3], y=[1, 3, 2])],
#         layout=PGraph.Layout(
#             title=PGraph.layout.Title(text="A Bar Chart")
#         )
# )

def main():
    fig = PGraph.Figure({
        "data": [{"type": "scatter",
                  "x": [0, 1, 2, 3],
                  "y": [100, 100, 50, 0]}],
        "layout": {
            "title": {"text": "Student Simulation with 20 sec Max Wait"},
            "xaxis": {
                "title": {"text": "Number of Students"},
                "range": [0,100]
            },
            "yaxis": {
                "title": {"text": "Percent of Executions with Runtime < 8 Sec "},
                "range": [0,100]
            },
        }
    })
    fig.show()
    # figure = express.scatter(x="The x-axis",y="The y-axis")

if __name__ == "__main__":
    main()