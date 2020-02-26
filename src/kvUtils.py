class kvUtils:
    @staticmethod
    def getTimeAsString(start_time, end_time):
        total_time = end_time - start_time;
        suffix = "s"
        if total_time < 1:
            total_time = total_time * 1000
            suffix = "ms"
        timeStr = str(total_time)
        timeStr = timeStr[:5] + suffix
        return timeStr
