from codeclient import CodeClient
import json

class Trial():
    def from_json(self,json_string):
        return json.loads(json_string)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"is_success" : self.is_success,
                "test_time" : self.test_time,
                "out" : self.out,
                "exp" : self.exp,
                "handler" : self.handler.to_dict(),
                "failure_reason" : self.failure_reason}


    def __init__(self,test_time=0,out='',exp='',timeout_response='',handler=None):
        self.is_success = (out == exp)
        self.test_time = test_time
        self.out = out
        self.exp = exp
        self.handler = handler
        if self.is_success:
            self.failure_reason = "None"
        elif self.out == timeout_response:
            self.failure_reason = "Timeout"
        else:
            self.failure_reason = "Wrong"

    def print(self):
        print("is_success: "+str(self.is_success))
        print("test_time: "+str(self.test_time))
        print("out: "+self.out.replace("\n","\\n"))
        print("exp: "+self.exp.replace("\n","\\n"))
        print("handler: "+str(self.handler.to_dict() if self.handler else str(None)))

    # def get_data_string(self):
    #     return  str(self.is_success) + "," \
    #             + str(self.test_time) + "," \
    #             + str("\'"+self.out.replace("\n","\\n")+"\'") + "," \
    #             + str("\'"+self.exp.replace("\n","\\n")+"\'") + "," \
    #             + str(self.failure_reason) + "," \
    #             + str(self.handler.run_time) + "," \
    #             + str(self.handler.send_time) + "," \
    #             + str(self.handler.recv_time) + "," \
    #             + str(self.handler.conn_attempt)

class Test():

    def log_test(self,file_name,should_append=True):
        mode = "a" if should_append else "w"

        with open(file_name,mode) as f:
            # print(test_name+"\n")
            f.write((self.to_json())+"\n")

    def from_json(self,json_string):
        return json.loads(json_string)

    def to_json(self):
        return json.dumps(self.to_dict())

    def from_dict(self,test_dict):
        return Test(test_dict["name"],
                    test_dict["test_type"],
                    test_dict["count"],
                    test_dict["interval"],
                    test_dict["time_limit"],
                    test_dict["trials"])

    def to_dict(self):
        # trials_dicts = [trial.to_dict() for trial in test.trials]
        #convert all trials into a {index:trial} dictionary
        trials_dict = { i : self.trials[i].to_dict()  for i in range(0, len(self.trials) ) }


        return {"name" : self.name,
                "test_type" : self.test_type,
                "count" : self.count,
                "interval" : self.interval,
                "time_limit" : self.time_limit,
                "trials" : trials_dict}

    def __init__(self,name,test_type,count,interval,time_limit,trials = []):
        self.name = name
        self.test_type = test_type
        self.count = count
        self.interval = interval
        self.time_limit = time_limit
        self.trials = trials

    def get_success_rate(self):
        total = len(self.trials)
        success = 0
        for trial in self.trials:
            if trial.is_success:
                success += 1
        return success/total


# def main():

# if __name__ == "__main__":
#     main()
