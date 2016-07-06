"""Tasks with ROS debugging machinery.

This is separate from the base task running machinery so that that can be tested
without ROS being involved.
"""
import rospy

from .tasks import TasksRunner

class RosTasksRunner(TasksRunner):
    @staticmethod
    def log(level, msg, *values):
        if level == 'fatal':
            rospy.logfatal(msg, *values)
        elif level == 'error':
            rospy.logerr(msg, *values)
        elif level == 'warning':
            rospy.logwarn(msg, *values)
        elif level == 'info':
            rospy.loginfo(msg, *values)
        else:
            rospy.logdebug(msg, *values)

    def register_debug_topics(self, topics)
        for (topic, datatype_s) in topics:
            if (topic in self.debug_topics) \
                    and (self.debug_topics[topic][0] == datatype_s):
                continue  # Already registered
            
            if ':' in topic:
                dt_mod, dt_cls = topic.split(':', 1)
            else:
                dt_mod = 'std_msgs.msg'
                dt_cls = topic
            mod = importlib.import_module(dt_mod)
            dt = getattr(mod, dt_cls)
            
            pub = rospy.Publisher(topic, dt, queue_size=10)
            self.debug_topics[topic] = (datatype_s, pub)
    
    def _make_task(self, taskdict):
        task = super(RosTasksRunner, self)._make_task(taskdict)
        
        self.register_debug_topics(task.debug_topics)
        task.log = self.log
        task.debug_pub = self.debug_pub
        return task
