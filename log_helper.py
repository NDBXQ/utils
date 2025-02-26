import logging
import sys


LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

LEVELS_ = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
"""
1. DEBUG:详细的信息，通常只在诊断问题时使用。
2. INFO:确认一切按预期工作的信息。
3. WARNING:表示某些意外情况或问题，但不会阻止程序继续运行。
4. ERROR:更严重的问题，表明程序不能执行某些功能。
5. CRITICAL:严重的错误，表明程序可能无法继续运行。

"""



#         grey = "\x1b[38;21m"
#         yellow = "\x1b[33;21m"
#         red = "\x1b[31;21m"
#         bold_red = "\x1b[31;1m"
#         reset = "\x1b[0m"

# ANSI转义码支持多种颜色。基本的文本颜色由以下码控制：

# 前景色（文字颜色）：30-37
# 背景色：40-47
# 每种颜色都有一个对应的数字：

# 30/40: 黑色
# 31/41: 红色
# 32/42: 绿色
# 33/43: 黄色
# 34/44: 蓝色
# 35/45: 紫红色
# 36/46: 青色（蓝绿色）
# 37/47: 白色
# 此外，你可以添加额外的属性，如：

# 1: 加粗
# 4: 下划线
# 7: 反白显示（反转前景色和背景色）



class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': "\x1b[35;24m",
        'INFO': "\x1b[40;49m",
        'WARNING': "\x1b[33;24m",
        'ERROR': "\x1b[31;24m",
        'CRITICAL': "\x1b[31;1m"
    }

    RESET = "\x1b[0m"

    def format(self, record):
        log_message = super().format(record)
        return self.COLORS.get(record.levelname, '') + log_message + self.RESET



class Log_Helper:
    def __init__(self,
            logger_name:str="my_logger",
            logger_level:str="INFO",
            handler_lever:str="INFO",
            log_file=None,
            event:str= None
            ):
        self.logger_name = logger_name
        self.logger_level = logger_level
        self.handler_lever = handler_lever
        self.log_file = log_file
        self.event = event
        self.logger = self.set_logger()

 

    def set_logger(self):
        """
        parameters:
            logger_name: logger name
            logger_level: logger level
            handler_lever: handler level
            log_file: log file path
        """
        logger = logging.getLogger(self.logger_name)

        
        
        if self.logger_level not in LEVELS:
            raise ValueError(f"Invalid logger level: {self.logger_level}. Choose from {LEVELS}")
        if self.handler_lever not in LEVELS:
            raise ValueError(f"Invalid handler level: {self.handler_lever}. Choose from {LEVELS}")


        logger.setLevel(LEVELS_[LEVELS.index(self.logger_level)])


        handler =  logging.FileHandler(self.log_file) if self.log_file else logging.StreamHandler(sys.stdout)


        if self.event:
            formatter = ColoredFormatter('%(asctime)s - %(name)s - Event::%(event)s - %(levelname)s - %(message)s ')
        else:
            formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger


    def debug(self, msg):
        if self.event:
            self.logger.debug(msg, extra={"event": self.event})
        else:
            self.logger.debug(msg)

    def info(self, msg):
        if self.event:
            self.logger.info(msg, extra={"event": self.event})
        else:
            self.logger.info(msg)

    def warning(self, msg):
        if self.event:
            self.logger.warning(msg, extra={"event": self.event})
        else:
            self.logger.error(msg)

    def error(self, msg):
        if self.event:
            self.logger.error(msg, extra={"event": self.event})
        else:
            self.logger.error(msg)
        
    def critical(self, msg):
        if self.event:
            self.logger.critical(msg, extra={"event": self.event})
        else:
            self.logger.critical(msg)


# if __name__ == "__main__":
#     logger = Log_Helper(logger_name="my_logger", logger_level="DEBUG", handler_lever="DEBUG", log_file="out.log", event="test")
#     # logger = Log_Helper(logger_name="my_logger", logger_level="DEBUG", handler_lever="DEBUG", event="test")

#     logger.debug("debug message")
#     logger.info("info message")
#     logger.warning("warning message")
#     logger.error("error message")
#     logger.critical("critical message")