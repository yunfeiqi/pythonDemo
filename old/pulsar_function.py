from pulsar import Function

class RoutingFunction(Function):
    def __init__(self):
        self.fruits_topic = "persistent://public/default/my-topic"


    def process(self, item, context):
        if len(item)>0:
            context.publish(self.fruits_topic, "1111111")
        else:
            warning = "The item {0} is neither a fruit nor a vegetable".format(item)
            context.get_logger().warn(warning)