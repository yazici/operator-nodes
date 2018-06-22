import bpy
from bpy.props import *
from .. base_node_types import ImperativeNode

class SpawnParticleNode(ImperativeNode, bpy.types.Node):
    bl_idname = "en_SpawnParticleNode"
    bl_label = "Spawn Particle Node"

    def get_particle_type_items(self, context):
        items = []
        for node in self.id_data.get_particle_type_nodes():
            items.append((node.type_name, node.type_name, ""))
        if len(items) == 0:
            items.append(("NONE", "NONE", ""))
        return items

    particle_type = EnumProperty(name = "Particle Type",
        items = get_particle_type_items)

    def create(self):
        self.new_input("en_ControlFlowSocket", "Previous")
        self.new_output("en_ControlFlowSocket", "Next", "NEXT")

    def draw(self, layout):
        layout.prop(self, "particle_type", text = "", icon = "MOD_PARTICLES")

    def get_code(self):
        if self.particle_type != "NONE":
            yield "SPAWN:{}:_new_particle".format(self.particle_type)
            yield "_new_particle.location = PARTICLE.location.copy()"
            yield "_new_particle.velocity = PARTICLE.velocity.copy()"
            yield "_new_particle.color = PARTICLE.color.copy()"
        yield "NEXT"