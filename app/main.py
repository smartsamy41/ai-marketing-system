from flow_controller import FlowController

flow = FlowController()


@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return flow.run_all(products)
