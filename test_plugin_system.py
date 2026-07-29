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

        "phone : string",

    ],

)

print()

print("🎉 Plugin System Working")