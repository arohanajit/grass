"""
GUI support functions


(C) 2008-2011 by the GRASS Development Team
This program is free software under the GNU General Public
License (>=v2). Read the file COPYING that comes with GRASS
for details.

:authors: Soeren Gebbert
"""

import grass.script as gs

from .core import get_available_temporal_mapsets, init_dbif
from .factory import dataset_factory

###############################################################################


def tlist_grouped(type, group_type: bool = False, dbif=None):
    """List of temporal elements grouped by mapsets.

    Returns a dictionary where the keys are mapset
    names and the values are lists of space time datasets in that
    mapset. Example:

    .. code-block:: python

        >>> import grass.temporal as tgis
        >>> tgis.tlist_grouped('strds')['PERMANENT']
        ['precipitation', 'temperature']

    :param type: element type (strds, str3ds, stvds)
    :param group_type: TBD

    :return: directory of mapsets/elements
    """
    result = {}
    _type = type
    dbif, connection_state_changed = init_dbif(dbif)

    mapset = None
    types = ["strds", "str3ds", "stvds"] if _type == "stds" else [_type]
    for _type in types:
        try:
            tlist_result = tlist(type=_type, dbif=dbif)
        except gs.ScriptError as e:
            gs.warning(e)
            continue

        for line in tlist_result:
            try:
                name, mapset = line.split("@")
            except ValueError:
                gs.warning(_("Invalid element '%s'") % line)
                continue

            if mapset not in result:
                if group_type:
                    result[mapset] = {}
                else:
                    result[mapset] = []

            if group_type:
                if _type in result[mapset]:
                    result[mapset][_type].append(name)
                else:
                    result[mapset][_type] = [
                        name,
                    ]
            else:
                result[mapset].append(name)

    if connection_state_changed is True:
        dbif.close()

    return result


###############################################################################


def tlist(type, dbif=None):
    """Return a list of space time datasets of absolute and relative time

    :param type: element type (strds, str3ds, stvds)

    :return: a list of space time dataset ids
    """
    _type = type
    id = None
    sp = dataset_factory(_type, id)
    dbif, connection_state_changed = init_dbif(dbif)

    mapsets = get_available_temporal_mapsets()

    output = []
    temporal_type = ["absolute", "relative"]
    for _type in temporal_type:
        # For each available mapset
        for mapset in mapsets.keys():
            # Table name
            if _type == "absolute":
                table = sp.get_type() + "_view_abs_time"
            else:
                table = sp.get_type() + "_view_rel_time"

            # Create the sql selection statement
            sql = "SELECT id FROM " + table
            sql += " WHERE mapset = '%s'" % (mapset)
            sql += " ORDER BY id"

            dbif.execute(sql, mapset=mapset)
            rows = dbif.fetchall(mapset=mapset)

            # Append the ids of the space time datasets
            for row in rows:
                for col in row:
                    output.append(str(col))

    if connection_state_changed is True:
        dbif.close()

    return output
