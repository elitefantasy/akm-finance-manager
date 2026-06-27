from kivy.metrics import dp, sp


# --------------------------------------------------
# Global UI Scale
# --------------------------------------------------

UI_SCALE = 1.0


# --------------------------------------------------
# Fonts
# --------------------------------------------------

class Font:
    SMALL = sp(14 * UI_SCALE)
    NORMAL = sp(16 * UI_SCALE)
    LARGE = sp(20 * UI_SCALE)
    TITLE = sp(24 * UI_SCALE)

    CARD_TITLE = sp(18 * UI_SCALE)
    CARD_VALUE = sp(30 * UI_SCALE)

    NAVIGATION = sp(16 * UI_SCALE)


# --------------------------------------------------
# Heights / Widths
# --------------------------------------------------

class Size:
    # Controls
    BUTTON_HEIGHT = dp(48 * UI_SCALE)
    TEXT_INPUT_HEIGHT = dp(48 * UI_SCALE)

    # Dashboard
    BALANCE_CARD_HEIGHT = dp(100 * UI_SCALE)
    STAT_CARD_HEIGHT = dp(90 * UI_SCALE)
    DASHBOARD_RECENT_HEIGHT = dp(320 * UI_SCALE)

    # Lists
    LIST_ITEM_HEIGHT = dp(45 * UI_SCALE)
    RECENT_ITEM_HEIGHT = dp(65 * UI_SCALE)

    # Navigation
    BOTTOM_NAV_HEIGHT = dp(80 * UI_SCALE)
    
    # Add Screen
    ADD_BALANCE_HEIGHT = dp(100 * UI_SCALE)

    # Add Screen
    ADD_RECENT_HEIGHT = dp(240 * UI_SCALE)

    ADD_BUTTON_HEIGHT = dp(48 * UI_SCALE)


# --------------------------------------------------
# Spacing
# --------------------------------------------------

class Spacing:
    SMALL = dp(8 * UI_SCALE)
    NORMAL = dp(12 * UI_SCALE)
    LARGE = dp(20 * UI_SCALE)


# --------------------------------------------------
# Padding
# --------------------------------------------------

class Padding:
    SCREEN = dp(16 * UI_SCALE)
    CARD = dp(12 * UI_SCALE)


class Border:
    CARD_WIDTH = dp(1)


# --------------------------------------------------
# Card Styling
# --------------------------------------------------

class Radius:
    CARD = dp(16 * UI_SCALE)


# --------------------------------------------------
# Colors
# --------------------------------------------------

class Color:
    # Navigation
    NAV_ACTIVE = (0.20, 0.50, 1.00, 1)
    NAV_INACTIVE = (0.30, 0.30, 0.30, 1)

    # Cards
    CARD = (0.15, 0.15, 0.15, 1)
    ADD_INPUT = (.12, .12, .12, 1)

    ADD_CARD = (.15, .15, .15, 1)

    ADD_BUTTON_INCOME = (0.00, 0.55, 0.00, 1)

    ADD_BUTTON_EXPENSE = (0.70, 0.00, 0.00, 1)

    # Text
    TEXT_PRIMARY = (1, 1, 1, 1)
    TEXT_SECONDARY = (0.70, 0.70, 0.70, 1)

    # Financial
    INCOME = (0.00, 1.00, 0.00, 1)
    EXPENSE = (1.00, 0.30, 0.30, 1)

    # Buttons
    PRIMARY = (0.20, 0.50, 1.00, 1)
    SUCCESS = (0.00, 0.60, 0.00, 1)
    DANGER = (0.70, 0.00, 0.00, 1)
    
   