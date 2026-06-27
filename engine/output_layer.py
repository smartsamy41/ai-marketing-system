class OutputLayer:

    def export(self, data):
        return {
            "status": "exported",
            "data": data
        }
