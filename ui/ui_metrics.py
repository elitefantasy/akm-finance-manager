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

    NAVIGATION = sp(18 * UI_SCALE)


# --------------------------------------------------
# Heights / Widths
# --------------------------------------------------

class Size:
    # Controls
    BUTTON_HEIGHT = dp(48 * UI_SCALE)
    TEXT_INPUT_HEIGHT = dp(48 * UI_SCALE)

    # Dashboard
    BALANCE_CARD_HEIGHT = dp(120 * UI_SCALE)
    STAT_CARD_HEIGHT = dp(110 * UI_SCALE)
    DASHBOARD_RECENT_HEIGHT = dp(320 * UI_SCALE)

    # Lists
    LIST_ITEM_HEIGHT = dp(45 * UI_SCALE)
    RECENT_ITEM_HEIGHT = dp(65 * UI_SCALE)

    # Navigation
    BOTTOM_NAV_HEIGHT = dp(72 * UI_SCALE)


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