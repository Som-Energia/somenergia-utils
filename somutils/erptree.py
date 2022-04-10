from yamlns import namespace as ns

def erptree(
        id, model,
        expand=None, # dict attribute -> model
        pickName=None, # fk atributes to pick the name
        pickId=None, # fk attributes to pick the id
        anonymize=None, # attributes to anonymize
        remove=None, # attributes to remove
        head=3, tail=3, # chars to leave when anonymizing
):
    """
    Retrieves an object from the erp and some children
    and does some common postprocessing to have
    a namespace that can be dumped as yaml.
    Children attributes are referenced by dot notation.
    - 'model' is the erppeek or ooop model factory.
    - 'expand' should be a dict of relation attributes
    to its erp model so that the tree can be expanded.
    - 'pickId' a list or space separated strings,
    for fk attributes you want to pick the id
    and remove the name.
    - 'pickName' is the counterpart, takes the name.
    - 'anonymize' will take any string attribute
    and will ellipse it but 'tail' chars from the end
    and 'head' chars from the beggining.
    - 'remove' will remove the attribute.
    """

    def processAttributes(attributes):
        """For each dotted attribute provides the containing
        parent object the name within the parent and the original
        full dotted name.
        """
        for attribute in listify(attributes):
            for context, leaf in  getContext(target, attribute):
                yield context, leaf, attribute

    target = ns(model.read(id))

    for context, leaf, fullname in processAttributes(expand):
        with step("Expanding", fullname):
            submodel = expand[fullname]
            oldvalue = context[leaf]
            if len(oldvalue)==2 and type(oldvalue[1]) == str:
                context[leaf] = ns(submodel.read(context[leaf][0]))
            else:
                context[leaf] = [ ns(x) for x in submodel.read(oldvalue)]

    for context, leaf, fullname in processAttributes(pickName):
        with step("FK as name", fullname):
            context[leaf] = context[leaf][1]

    for context, leaf, fullname in processAttributes(pickId):
        with step("FK as id", fullname):
            context[leaf] = context[leaf][0]

    for context, leaf, fullname in processAttributes(anonymize):
        with step("Anonymizing", fullname):
            val = str(context[leaf])
            context[leaf] = val[:head] + "..." + val[-tail:]

    for context, leaf, fullname in processAttributes(remove):
        with step("Removing", fullname):
            if type(context) == list:
                for x in context:
                    del x[leaf]
            else:
                del context[leaf]

    return target

from contextlib import contextmanager


@contextmanager
def step(doing, attribute):
    #print(doing, attribute)
    try:
        yield
    except Exception as e:
        print("Error while", doing, attribute)
        raise


def listify(attributes):
    """
    If the param evals to false, it returns an empty list.
    If the param is a string, it returns it splited and sorted.
    Else it takes the param as an iterable and returns it sorted.

    >>> listify('element')
    ['element']
    >>> listify('element2 element1')
    ['element1', 'element2']
    >>> listify(['element2', 'element1'])
    ['element1', 'element2']
    >>> listify([])
    []
    >>> listify(None)
    []
    """

    if not attributes:
        return []
    if type(attributes) == str:
        return sorted(attributes.split())
    return sorted(attributes)


def getContext(o, attribute):
    """
    Given the structure `o`, and a dotted attribute path,
    returns the inmediate parents having the attribute and the leave attribute name.

    So given the structure:

    >>> data = ns.loads('''
    ...   attrib1:
    ...     attrib11: value11
    ...     attrib12: value12
    ...   attrib2:
    ...     - attrib21: valueItem0
    ...     - attrib21: valueItem1
    ...   attrib3:
    ...     - attrib31:
    ...         attrib311: valueItem0
    ...     - attrib31:
    ...         attrib311: valueItem1
    ... ''')

    You get:

    >>> list(getContext(data, 'attrib1')) == [(data, 'attrib1')]
    True
    >>> list(getContext(data.attrib1, 'attrib11')) == [(data.attrib1, 'attrib11')]
    True
    >>> list(getContext(data, 'attrib1.attrib11')) == [(data.attrib1, 'attrib11')]
    True
    >>> list(getContext(data.attrib2, 'attrib21')) ==  [
    ...     (data.attrib2[0], 'attrib21'),
    ...     (data.attrib2[1], 'attrib21'),
    ... ]
    True
    >>> list(getContext(data, 'attrib2.attrib21')) == [
    ...     (data.attrib2[0], 'attrib21'),
    ...     (data.attrib2[1], 'attrib21'),
    ... ]
    True
    >>> list(getContext(data, 'attrib3.attrib31.attrib311')) == [
    ...     (data.attrib3[0].attrib31, 'attrib311'),
    ...     (data.attrib3[1].attrib31, 'attrib311'),
    ... ]
    True
    """

    if type(o) == list:
        for item in o:
            # TODO: substitute by "yield from" on Py2 dropped
            for x in getContext(item, attribute):
                yield x
        return

    steps = attribute.split('.', 1)
    thisStep, remaining = steps[0], steps[1:]
    if not remaining:
        yield o, thisStep
        return

    # TODO: substitute by "yield from" on Py2 dropped
    for x in getContext(o[thisStep], remaining[0]):
        yield x



