import omni.ext
import omni.kit.viewport.utility
import omni.ui as ui
import omni.usd
import omni.kit.viewport
from pxr import Usd, UsdGeom
import asyncio


class OrdinarySceneDisappearingExtension(omni.ext.IExt):

    def on_startup(self, ext_id):
        print("[ordinary.scene.disappearing] ordinary scene disappearing startup")

        self._stage = omni.usd.get_context().get_stage()

        # This is the string model used by the string input field.
        self._base_path_model = ui.SimpleStringModel("/World/Boxes")

        self._window = ui.Window("Capture Disappearing Things", width=300, height=150)
        with self._window.frame:
            with ui.VStack(spacing=2):
                label = ui.Label("Path for objects to hide: " + self._base_path_model.get_value_as_string(), height=25)

                with ui.HStack(height=25):
                    ui.Label("Enter Base Path: ")
                    ui.StringField(self._base_path_model)

                def on_capture_click():
                    asyncio.ensure_future(self.capture_disappearing_scene())

                def on_reset_click():
                    self.reset_disappearing_scene()

                with ui.HStack():
                    ui.Button("Capture", clicked_fn=on_capture_click)
                    ui.Button("Reset", clicked_fn=on_reset_click)

    async def capture_disappearing_scene(self):
        stage: Usd.Stage = self._stage
        root_layer = stage.GetRootLayer()
        with Usd.EditContext(stage, root_layer):
            base: Usd.Prim = stage.GetPrimAtPath(self._base_path_model.get_value_as_string())
            if base:
                i = 0
                await self.snapshot(i)
                child: Usd.Prim
                for child in base.GetAllChildren():
                    i += 1
                    UsdGeom.Imageable(child).GetVisibilityAttr().Set('invisible')
                    await self.snapshot(i)

    async def snapshot(self, i: int):
        # Wait 10 frames to give renderer a chance to finish
        for _ in range(10):
            await omni.kit.app.get_app().next_update_async()
        frame_file = f"frame_{i:04}.png"
        viewport = omni.kit.viewport.utility.get_active_viewport()
        omni.kit.viewport.utility.capture_viewport_to_file(viewport, frame_file)

    def reset_disappearing_scene(self):
        stage: Usd.Stage = self._stage
        root_layer = stage.GetRootLayer()
        with Usd.EditContext(stage, root_layer):
            base: Usd.Prim = stage.GetPrimAtPath(self._base_path_model.get_value_as_string())
            if base:
                child: Usd.Prim
                for child in base.GetAllChildren():
                    UsdGeom.Imageable(child).GetVisibilityAttr().Set('inherited')

    def on_shutdown(self):
        print("[ordinary.scene.disappearing] ordinary scene disappearing shutdown")
