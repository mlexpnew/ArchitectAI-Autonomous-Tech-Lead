from plugins.plugin_manager import PluginManager

manager = PluginManager(
    "outputs/Hospital_Management_System",
)

manager.execute(
    "model",
    "Patient",
    [
        "id : integer",
        "name : string",
        "age : integer",
    ],
)

manager.execute(
    "schema",
    "Patient",
    [
        "id : integer",
        "name : string",
        "age : integer",
    ],
)

manager.execute(
    "model",
    "Patient",
    [
        "id : integer",
        "name : string",
        "age : integer",
    ],
)