import arcade
import arcade.gui
from arcade import key

from W_Main_File.Utilities import Button_Functions, Action_Queue, Custom_Menu
from W_Main_File.Views import Purgatory_Screen, Event_Base, TileRenderer
from W_Main_File.Data import Sprites_, Item
from W_Main_File.Essentials import State
import time
import random
from W_Main_File.Tiles import Loot_Functions, Trapdoor_Functions, Trap_Functions, Enemy
from W_Main_File.Utilities.Vector import Vector


class Explore(Event_Base.EventBase):
    fps = 0
    last_update = 0
    symbol_ = arcade.key.D
    previous_pos = Vector(0, 0)
    current_window_size = Vector(1000, 800)

    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        if not State.state.preoccupied:
            self.ui_manager.purge_ui_elements()
        Button_Functions.register_custom_exploration_buttons(self.button_manager, self.ui_manager)
        State.state.is_moving = False
        if ((State.state.moves_since_texture_save > 2 and State.state.is_new_tile) or State.state.player.pos == (0, 0)) and not State.state.player.meta_data.is_guest:
            for offset in State.state.generate_radius(5):
                State.state.tile_type_pos(*(offset + State.state.player.pos))
            State.state.is_new_tile = False
            State.state.moves_since_texture_save = 0
        self.should_transition_to_animation = [False, 0, 0, lambda: None]
        if not State.state.grid.get(-1, 0):
            State.state.grid.add(Trapdoor_Functions.TrapdoorTile(Vector(-1, 0)))
        if not State.state.grid.get(2, 0):
            State.state.grid.add(Loot_Functions.LootTile(Vector(2, 0)))
        from W_Main_File.Items import Inventory
        self.yfes = False
        self.delta = time.time()
        arcade.set_background_color((0, 0, 0))
        self.tile_renderer = TileRenderer.TileRenderer(State.state.render_radius)
        # self.button_manager.append('Up', 'Up',
        #                            Vector((State.state.window.width * 0.875),
        #                                   (State.state.screen_center.y - (State.state.window.height * 0.3125)) + (State.state.cell_render_size.y - (State.state.window.height * 0.03))),
        #                            Vector((State.state.window.width * 0.2), (State.state.window.height * 0.0625)), on_click=lambda:self.on_key_press(arcade.key.W, 0))
        if Event_Base.symbols:
            syms = (list(Event_Base.symbols & {arcade.key.A, arcade.key.D, arcade.key.W, arcade.key.S}))
            if syms:
                self.on_key_press(syms[0], Event_Base.held_modifiers)
        State.cache_state.prior_player_grid_pos = State.state.player.pos.rounded()
        State.cache_state.prior_camera_pos = State.state.camera_pos
        State.cache_state.trap_additive_distance = 0
        self.menu_manager = Custom_Menu.MenuManager()

    def update(self, delta_time: float):
        self.delta = delta_time
        from W_Main_File.Views import Fading
        if State.state.player.hp <= 0:
            State.state.window.show_view(Fading.Fading((lambda: Purgatory_Screen.PurgatoryScreen('You Died', True)), 7, 4, should_reverse=False,
                                                       should_freeze=True, reset_pos=Vector(0, 0), render=lambda _: self.on_draw()))
            State.state.clear_current_floor_data()
        self.check_action_queue()
        # if self.should_transition_to_animation[0]:
        #     TO DO
        #     self.should_transition_to_animation[0] = False
        #     self.should_transition_to_animation[3]()
        # else:
        Sprites_.update_backdrop()
        self.check_if_resized()
        if Explore.last_update == 0 or time.time() - Explore.last_update > 0.5:
            Explore.fps = 1 / delta_time
            Explore.last_update = time.time()

        for x_off, y_off in State.state.generate_radius(State.state.render_radius):
            real_grid_pos = State.state.player.pos + (x_off, y_off)

            if tile := State.state.grid.get(*real_grid_pos):
                tile.on_update(delta_time)
        if State.state.preoccupied:
            return
        run_once = False
        for symbol in tuple(Event_Base.symbols):
            if symbol in self.key_offset:
                State.state.player.pos = (State.state.camera_pos / State.state.cell_render_size).rounded()
                State.state.camera_pos += (Vector(*self.key_offset[symbol]) * self.movement_speed) * self.delta
                if (State.state.texture_mapping[f'{State.state.player.pos.x} {State.state.player.pos.y}']) in Sprites_.trap_options:
                    if not isinstance(State.state.grid.get(*State.state.player.pos), Trap_Functions.TrapTile):
                        tile = Trap_Functions.TrapTile(State.state.player.pos)
                        State.state.grid.add(tile)
                    else:
                        tile = State.state.grid.get(*State.state.player.pos)
                    if State.cache_state.trap_additive_distance > 75:
                        State.cache_state.trap_additive_distance = 0
                        Action_Queue.action_queue.append(tile.on_enter)
                    elif not run_once:
                        State.cache_state.trap_additive_distance += ((Vector(*self.key_offset[symbol]) * self.movement_speed) * self.delta).distance()
                    print(State.cache_state.trap_additive_distance)
                elif State.cache_state.trap_additive_distance:
                    State.cache_state.trap_additive_distance = 0
                if (State.state.texture_mapping[f'{State.state.player.pos.x} {State.state.player.pos.y}']) in Sprites_.trapdoor_options:
                    if not isinstance(State.state.grid.get(*State.state.player.pos), Trapdoor_Functions.TrapdoorTile):
                        if not State.state.grid.get(*State.state.player.pos):
                            State.state.grid.add(Trapdoor_Functions.TrapdoorTile(State.state.player.pos))
                if State.state.player.pos.tuple() != State.cache_state.prior_player_grid_pos.tuple():
                    if tile := State.state.grid.get(*State.cache_state.prior_player_grid_pos.tuple()):
                        if not tile.can_player_move():
                            break
                        tile.on_exit()
                    if tile := State.state.grid.get(*State.state.player.pos):
                        if State.state.get_tile_id(State.state.player.pos) not in Sprites_.trap_options:
                            Action_Queue.action_queue.append(tile.on_enter)
                self.gen_new_inter_tiles(symbol)
                run_once = True
        if Action_Queue.action_queue:
            Action_Queue.action_queue.popleft()()

        if any(symbol for symbol in Event_Base.symbols if symbol in self.key_offset):
            Sprites_.update_character()
        State.cache_state.prior_player_grid_pos = State.state.player.pos
        State.cache_state.prior_camera_pos = State.state.camera_pos

    def check_if_resized(self):
        if self.current_window_size.xf == State.state.window.width and self.current_window_size.yf == State.state.window.height:
            return
        else:
            Button_Functions.register_custom_exploration_buttons(self.button_manager, self.ui_manager)
            self.current_window_size = Vector(State.state.window.width, State.state.window.height)
        from W_Main_File.Utilities import Inventory_GUI
        if Inventory_GUI.is_inv():
            Inventory_GUI.hide_inv(self.button_manager)
            Inventory_GUI.show_inv(self.button_manager)

    key_offset = {
        key.W: (0, 1),
        key.A: (-1, 0),
        key.S: (0, -1),
        key.D: (1, 0)
    }

    movement_speed = 200

    # noinspection PyProtectedMember
    def on_draw(self):
        arcade.start_render()
        center_screen = State.state.screen_center
        cell_render_size = (State.state.cell_size * ((State.state.window.width / State.state.default_window_size.xf), (State.state.window.height / State.state.default_window_size.y)))
        # TODO fix stuff around here
        self.tile_renderer.on_draw(State.state.render_radius)
        self.tile_renderer.on_draw_tile()
        arcade.draw_texture_rectangle(State.state.screen_center.xf, State.state.screen_center.yf,
                                      State.state.cell_render_size.xf * 0.73, State.state.cell_render_size.yf * 0.88, Sprites_.black_circle_sprite, 0, 75)
        arcade.draw_texture_rectangle(State.state.screen_center.xf, State.state.screen_center.yf,
                                      State.state.cell_render_size.xf * 0.73, State.state.cell_render_size.yf * 0.88, Sprites_.black_circle_square_sprite, 0, 100)
        arcade.draw_texture_rectangle(State.state.screen_center.xf, State.state.screen_center.yf,
                                      State.state.cell_render_size.xf * 0.73, State.state.cell_render_size.yf * 0.88, Sprites_.black_square_circle_square_sprite, 0, 125)

        arcade.draw_rectangle_filled(center_screen.xf, center_screen.yf - (State.state.window.height * 0.3375), State.state.window.width * 0.625, State.state.window.height * 0.0475, (0, 0, 0))
        arcade.draw_rectangle_filled(center_screen.xf, center_screen.yf + (State.state.window.height * 0.3375), State.state.window.width * 0.625, State.state.window.height * 0.0475, (0, 0, 0))
        # arcade.draw_circle_filled(center_screen.xf, center_screen.yf, 25, arcade.color.AERO_BLUE)
        screen_percentage_of_default = (State.state.window.height / State.state.default_window_size.y)
        arcade.draw_text(f'Floor: {int(State.state.player.floor)}', State.state.window.width * 0.5,
                         (State.state.window.height * 0.5) - (cell_render_size.yf * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=(12 * screen_percentage_of_default), anchor_x='center', anchor_y='center')
        arcade.draw_text(str(State.state.player.pos), State.state.window.width * 0.5,
                         (State.state.window.height * 0.5) + (cell_render_size.yf * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=(12 * screen_percentage_of_default), anchor_x='center', anchor_y='center')
        if not any(symbol for symbol in Event_Base.symbols if symbol in self.key_offset):
            if Explore.symbol_ == arcade.key.D:
                arcade.draw_texture_rectangle(State.state.screen_center.xf, State.state.screen_center.yf,
                                              State.state.cell_render_size.yf * 0.75, State.state.cell_render_size.yf * 0.75, Sprites_.knight_start_2)
            elif Explore.symbol_ == arcade.key.A:
                arcade.draw_texture_rectangle(State.state.screen_center.xf, State.state.screen_center.yf,
                                              State.state.cell_render_size.yf * 0.75, State.state.cell_render_size.yf * 0.75, Sprites_.knight_start_flipped)
        else:
            Sprites_.draw_character()
        Sprites_.draw_backdrop()
        arcade.draw_rectangle_outline(center_screen.xf, center_screen.yf, State.state.window.width * 0.5, State.state.window.height * 0.625, (120, 120, 120), 4)
        from W_Main_File.Utilities import Inventory_GUI
        arcade.draw_text(f'FPS = {self.fps:.1f}', 2, self.window.height - 22, arcade.color.GREEN,
                         font_name='arial', font_size=14)
        self.tile_renderer.on_draw_foreground()
        self.text_render()
        # if State.state.preoccupied:
        #     arcade.draw_text('Preoccupied', 800, 700, arcade.color.RED, 30)
        self.button_manager.render()
        Inventory_GUI.render_inventory(Vector(self.window._mouse_x, self.window._mouse_y))
        if menu := self.menu_manager.display_menu('Inv_Item_Menu'):
            arcade.draw_line(menu.pos.x+10, menu.pos.y-3, menu.pos.x+10, menu.pos.y - (25 * 1), arcade.color.RED, 3)
            arcade.draw_line(menu.pos.x + 10, menu.pos.y - (25 * 1), menu.pos.x + 10, menu.pos.y - (25 * 2), arcade.color.WHITE, 3)
            arcade.draw_line(menu.pos.x + 10, menu.pos.y - (25 * 2), menu.pos.x + 10, menu.pos.y - (25 * 3), arcade.color.RED, 3)
            arcade.draw_line(menu.pos.x + 10, menu.pos.y - (25 * 3), menu.pos.x + 10, menu.pos.y - (25 * 4), arcade.color.WHITE, 3)
            arcade.draw_line(menu.pos.x + 10, menu.pos.y - (25 * 4), menu.pos.x + 10, menu.pos.y - (25 * 5), arcade.color.RED, 3)
        arcade.draw_point(State.state.screen_center.x, State.state.screen_center.y, arcade.color.RED, 4)
        if Inventory_GUI.is_inv():
            if Inventory_GUI._menu_toggle:
                State.state.render_mouse()
        else:
            State.state.render_mouse()

    # noinspection PyMethodMayBeStatic
    def text_render(self):
        screen_percentage_of_default = (State.state.window.height / State.state.default_window_size.y)
        arcade.draw_text(f'Name: {State.state.player.name}', State.state.window.width * 0.275, State.state.window.height * 0.1625, arcade.color.LIGHT_GRAY,
                         font_size=(11 * screen_percentage_of_default), font_name='arial')
        arcade.draw_text(f'Hp: {int(State.state.player.hp)} / {int(State.state.player.max_hp)}', State.state.window.width * 0.475, State.state.window.height * 0.1625, arcade.color.LIGHT_GRAY,
                         font_size=(11 * screen_percentage_of_default), font_name='arial')
        arcade.draw_text(f'Level: {int(State.state.player.lvl)}', State.state.window.width * 0.67, State.state.window.height * 0.1625, arcade.color.LIGHT_GRAY,
                         font_size=(11 * screen_percentage_of_default), font_name='arial')
        arcade.draw_text(f'Gold: {int(State.state.player.gold)}', State.state.window.width * 0.355, State.state.window.height * 0.8125, arcade.color.LIGHT_GRAY,
                         font_size=(14 * screen_percentage_of_default), font_name='arial')
        arcade.draw_text(f'xp: {int(State.state.player.xp)}', State.state.window.width * 0.565, State.state.window.height * 0.8125, arcade.color.LIGHT_GRAY,
                         font_size=(14 * screen_percentage_of_default), font_name='arial')
    def on_key_release(self, symbol, mods):
        super().on_key_release(symbol, mods)
        if tile := State.state.grid.get(*State.state.player.pos):
            tile.key_up(symbol, mods)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        from W_Main_File.Utilities import Inventory_GUI
        if button == arcade.MOUSE_BUTTON_RIGHT:
            if Inventory_GUI.is_inv():
                Inventory_GUI._menu_toggle = True
                item = Inventory_GUI.get_hovered_item(Vector(x, y))
                gvacfi = self.get_values_and_callbacks_from_item(item)
                if gvacfi is not None:
                    self.menu_manager.make_menu('Inv_Item_Menu', Vector(x, y), '', 'Title', gvacfi, True)
                else:
                    if self.menu_manager.check_if_mouse_on_menu('Inv_Item_Menu', Vector(x, y)):
                        self.menu_manager.remove_menu('Inv_Item_Menu')
                # TODO
        else:
            if not self.menu_manager.check_if_mouse_on_menu('Inv_Item_Menu', Vector(x, y)):
                Inventory_GUI._menu_toggle = False
                self.menu_manager.remove_menu('Inv_Item_Menu')
        if button == arcade.MOUSE_BUTTON_LEFT:
            if Inventory_GUI.is_inv() and self.menu_manager.check_if_mouse_on_menu('Inv_Item_Menu', Vector(x, y)):
                menu = self.menu_manager.menus['Inv_Item_Menu']
                rel_mouse_pos = Vector(x - menu.pos.x, abs(menu.pos.y - y))
                gvacfi_2 = self.get_values_and_callbacks_from_item(Inventory_GUI.get_hovered_item(Vector(x, y)))


    def get_values_and_callbacks_from_item(self, item: Item.Item):
        if item:
            if item.type_ == Item.ItemType.Weapon:
                return {'trash': lambda: State.state.inventory.remove_item_not_index(item), 'sell': lambda: None}
            elif item.type_ == Item.ItemType.Armour:
                return {'trash': lambda: State.state.inventory.remove_item_not_index(item), 'sell': lambda: None}
            elif item.type_ == Item.ItemType.Accessory:
                return {'trash': lambda: State.state.inventory.remove_item_not_index(item), 'sell': lambda: None}
            elif item.type_ == Item.ItemType.Consumable:
                return {'trash': lambda: State.state.inventory.remove_item_not_index(item), 'sell': lambda: None}
        else:
            return None

    def check_action_queue(self):
        while Action_Queue.action_queue:
            action = Action_Queue.action_queue.popleft()
            action()

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)
        if symbol == arcade.key.B:
            State.state.player.hp -= State.state.player.max_hp
        if symbol == arcade.key.L:
            self.yes = True
        if symbol == arcade.key.I:
            if modifiers & arcade.key.MOD_SHIFT:
                for num in range(0, 10):
                    from W_Main_File.Items import All_Items
                    State.state.inventory.items.append(random.choice((All_Items.rusty_knife, All_Items.null_weapon_1, All_Items.null_weapon_2)))
            else:
                for num in range(0, 3):
                    from W_Main_File.Items import All_Items
                    State.state.inventory.items.append(random.choice((All_Items.rusty_knife, All_Items.null_weapon_1, All_Items.null_weapon_2)))
        if symbol in self.key_offset:
            if symbol in (arcade.key.A, arcade.key.D):
                self.__class__.symbol_ = symbol

            if State.state.preoccupied:
                return
            self.__class__.previous_pos = State.state.player.pos
            State.state.moves_since_texture_save += 1
            offset = ((Vector(*self.key_offset[symbol]) * self.movement_speed) * self.delta / State.state.cell_render_size).rounded()
            prior_player_pos = State.state.player.pos
            new_player_pos = prior_player_pos + offset
            prev_tile = State.state.grid.get(*prior_player_pos)
            new_tile = State.state.grid.get(*new_player_pos)
            if prev_tile and not new_tile:
                if not prev_tile.can_player_move():
                    return
                prev_tile.on_exit()
            if new_tile != prev_tile and new_tile:
                new_tile.on_enter()

        else:
            if tile := State.state.grid.get(*State.state.player.pos):
                tile.key_down(symbol, modifiers)

    def gen_new_inter_tiles(self, symbol):
        self.__class__.previous_pos = State.state.player.pos
        State.state.moves_since_texture_save += 1
        offset = ((Vector(*self.key_offset[symbol]) * self.movement_speed) * self.delta / State.state.cell_render_size).rounded()
        prior_player_pos = State.state.player.pos
        new_player_pos = prior_player_pos + offset
        prev_tile = State.state.grid.get(*prior_player_pos)
        new_tile = State.state.grid.get(*new_player_pos)
        if prev_tile and not new_tile:
            if not prev_tile.can_player_move():
                return
            prev_tile.on_exit()
        if new_tile != prev_tile and new_tile:
            new_tile.on_enter()

        def after_update():
            if State.state.player.pos.tuple() not in State.state.grid.visited_tiles:
                State.state.player.pos = new_player_pos
                if (
                        not State.state.grid.get(new_player_pos.x, new_player_pos.y)
                        and random.random() < 0.2
                        and State.state.texture_mapping.get(f'{new_player_pos.x} {new_player_pos.y}') in Sprites_.loot_options
                        and new_player_pos.tuple() not in State.state.grid.visited_tiles
                ):
                    loot = Loot_Functions.LootTile(new_player_pos)
                    State.state.grid.add(loot)
                elif (
                        not State.state.grid.get(new_player_pos.x, new_player_pos.y)
                        and random.random() < 0.05
                        and State.state.texture_mapping.get(f'{new_player_pos.x} {new_player_pos.y}') in Sprites_.enemy_options
                        and new_player_pos.tuple() not in State.state.grid.visited_tiles
                ):
                    enemy = Enemy.EnemyTile(new_player_pos)
                    State.state.grid.add(enemy)
                elif (
                        State.state.get_tile_id(Vector(new_player_pos.x, new_player_pos.y)) == Sprites_.trapdoor_options
                        and not State.state.grid.get(new_player_pos.x, new_player_pos.y)
                ):
                    trapdoor = Trapdoor_Functions.TrapdoorTile(Vector(new_player_pos.x, new_player_pos.y))
                    State.state.grid.add(trapdoor)
                State.state.grid.add_visited_tile(new_player_pos)

        after_update()
        self.check_action_queue()
