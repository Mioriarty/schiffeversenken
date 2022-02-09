import weakref

class InstanceRegistryMetaClass(type):

    @staticmethod
    def lookForRootRegistry(cls, bases):
        for b in bases:
            if '__is_registry__' in b.__dict__:
                return InstanceRegistryMetaClass.lookForRootRegistry(b, b.__bases__)
        return cls

    def __init__(cls, name, bases, attrs):
        # default class creation
        super(InstanceRegistryMetaClass, cls).__init__(name, bases, attrs)

        # add property to specify that this class has used this metclass
        cls.__is_registry__ = True

        # look for root level registry
        rootCls = InstanceRegistryMetaClass.lookForRootRegistry(cls, bases)

        if rootCls == cls:
            # create registry
            cls._instances = weakref.WeakSet()
            cls.getInstances = lambda : list(cls._instances)

            def clearInstances():
                cls._instances = weakref.WeakSet()

            cls.clearInstances = clearInstances

        cls.__registerInstance = lambda i : rootCls._instances.add(i)


    
    def __call__(cls, *args, **kwargs):
        # default instance creation
        instance = super(InstanceRegistryMetaClass, cls).__call__(*args, **kwargs)

        # add to registry
        cls.__registerInstance(instance)

        return instance
