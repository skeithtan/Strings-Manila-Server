class StoreStatus:
    on_maintenance = True

    @staticmethod
    def enable_maintenance():
        StoreStatus.on_maintenance = True

    @staticmethod
    def disable_maintenance():
        StoreStatus.on_maintenance = False
