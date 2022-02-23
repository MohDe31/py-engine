import core.application

def init(application: core.application.Application):
    # TODO Pack this stuff
    application.m_ActiveScene = core.scene.Scene()
    camera_entity = application.m_ActiveScene.makeEntity()
    tr_ = camera_entity.addComponent(core.components.transform.Transform, *([0]*6))
    camera_entity.addComponent(core.components.camera.Camera, 45.0, application.WIDTH / application.HEIGHT)

    tr_.setPosition(0,   0, 5)
    tr_.setRotation(0, -90, 0)

    for _ in range(500):
        application.createBuffer()

def update(dt: float):
    pass

if __name__ == "__main__":
    (core.application.Application(init=init)).run(update=update)
