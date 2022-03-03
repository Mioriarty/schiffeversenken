import weakref

class InstanceRegistryMetaClass(type):
    """
    Metaclass that creates a protected static _instances property for the class that keeops track of all created instances.
    """

    @staticmethod
    def __lookForRootRegistry(cls : type, bases : tuple[type]) -> type:
        """
        Looks for the root registry so that deriving classes also register in the top most registry.

        Args:
            cls (type): The current class we are abserving.
            bases (tuple[type]): All base classes of the cls.

        Returns:
            type: The class that holds the root registry.
        """
        for b in bases:
            if '__is_registry__' in b.__dict__:
                return InstanceRegistryMetaClass.__lookForRootRegistry(b, b.__bases__)
        return cls

    def __init__(cls, name : str, bases : tuple[type], attrs : dict):
        """
        Handles the class creation. (standart metaclass method)

        Args:
            name (str): The name of the class to be created
            bases (tuple[type]): All its base class.
            attrs (dict): All its attributes.
        """
        # default class creation
        super(InstanceRegistryMetaClass, cls).__init__(name, bases, attrs)

        # add property to specify that this class has used this metclass
        cls.__is_registry__ = True

        # look for root level registry
        rootCls = InstanceRegistryMetaClass.__lookForRootRegistry(cls, bases)

        if rootCls == cls:
            # create registry
            cls._instances = weakref.WeakSet()
            cls.getInstances = lambda : list(cls._instances)

            def clearInstances():
                cls._instances = weakref.WeakSet()

            cls.clearInstances = clearInstances

        cls.__registerInstance = lambda i : rootCls._instances.add(i)


    
    def __call__(cls, *args, **kwargs):
        """
        Handles instance creation of the class.

        Args:
            *args: Non-keyword arguments
            **kwargs: Keyword arguments

        Returns:
            A new registered instance of the class.
        """
        # default instance creation
        instance = super(InstanceRegistryMetaClass, cls).__call__(*args, **kwargs)

        # add to registry
        cls.__registerInstance(instance)

        return instance
