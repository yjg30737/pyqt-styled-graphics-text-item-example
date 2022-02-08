from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPen, QPainter, QColor, QCursor
from PyQt5.QtWidgets import QGraphicsView, QMainWindow, QApplication, QGraphicsItem, QGraphicsScene, \
    QGraphicsTextItem, QWidget, QStyleOptionGraphicsItem


class Box(QGraphicsTextItem):
    def __init__(self):
        super().__init__()
        self.__line_width = 1
        self.__resized = False

        self.__margin = self.__line_width + 2
        self.__cursor = QCursor()

        self.__initPosition()
        self.__initUi()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        pen = QPen(QColor('#DDDDDD'), self.__line_width)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(pen)
        painter.setBrush(Qt.cyan)
        self.__boundingRect = self.boundingRect()
        painter.drawRoundedRect(self.__boundingRect, 5.0, 5.0)

        return super().paint(painter, option, widget)

    def __initUi(self):
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)

    # init the edge direction for set correct reshape cursor based on it
    def __initPosition(self):
        self.__top = False
        self.__bottom = False
        self.__left = False
        self.__right = False

    def __setCursorShapeForCurrentPoint(self, p):
        # give the margin to reshape cursor shape
        boundingRect = self.boundingRect()
        boundingRect.setX(self.boundingRect().x() + self.__margin)
        boundingRect.setY(self.boundingRect().y() + self.__margin)
        boundingRect.setWidth(self.boundingRect().width() - self.__margin * 2)
        boundingRect.setHeight(self.boundingRect().height() - self.__margin * 2)

        self.__resized = boundingRect.contains(p)
        if self.__resized:
            # resize end
            self.unsetCursor()
            self.__cursor = self.cursor()
            self.__initPosition()
        else:
            # resize start
            x = p.x()
            y = p.y()

            x1 = self.boundingRect().x()
            y1 = self.boundingRect().y()
            x2 = self.boundingRect().width()
            y2 = self.boundingRect().height()

            self.__left = abs(x - x1) <= self.__margin # if mouse cursor is at the almost far left
            self.__top = abs(y - y1) <= self.__margin # far top
            self.__right = abs(x - (x2 + x1)) <= self.__margin # far right
            self.__bottom = abs(y - (y2 + y1)) <= self.__margin # far bottom

            # set the cursor shape based on flag above
            if self.__top and self.__left:
                self.__cursor.setShape(Qt.SizeFDiagCursor)
            elif self.__top and self.__right:
                self.__cursor.setShape(Qt.SizeBDiagCursor)
            elif self.__bottom and self.__left:
                self.__cursor.setShape(Qt.SizeBDiagCursor)
            elif self.__bottom and self.__right:
                self.__cursor.setShape(Qt.SizeFDiagCursor)
            elif self.__left:
                self.__cursor.setShape(Qt.SizeHorCursor)
            elif self.__top:
                self.__cursor.setShape(Qt.SizeVerCursor)
            elif self.__right:
                self.__cursor.setShape(Qt.SizeHorCursor)
            elif self.__bottom:
                self.__cursor.setShape(Qt.SizeVerCursor)
            self.setCursor(self.__cursor)

        self.__resized = not self.__resized

    def keyPressEvent(self, e):
        tr = self.transform()
        if e.key() == Qt.Key_Up:
            tr.translate(0, -1)
        if e.key() == Qt.Key_Down:
            tr.translate(0, 1)
        if e.key() == Qt.Key_Left:
            tr.translate(-1, 0)
        if e.key() == Qt.Key_Right:
            tr.translate(1, 0)
        self.setTransform(tr)
        return super().keyPressEvent(e)

    def mouseMoveEvent(self, e):
        self.__setCursorShapeForCurrentPoint(e.pos())
        return super().mouseMoveEvent(e)

    def mouseDoubleClickEvent(self, e):
        super().mouseDoubleClickEvent(e)
        if e.button() == Qt.LeftButton:
            self.setTextInteractionFlags(Qt.TextEditable)
            self.setFocus()

    def focusOutEvent(self, e):
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        return super().focusOutEvent(e)

    def hoverMoveEvent(self, e):
        p = e.pos()

        if self.boundingRect().contains(p):
            self.__setCursorShapeForCurrentPoint(p)

        return super().hoverMoveEvent(e)


class StyleGraphicsTextItemExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        view = QGraphicsView()

        self.__scene = QGraphicsScene()
        self.__scene.setSceneRect(0, 0, 400, 400)

        box1 = Box()
        box1.setPlainText('Box1')

        box2 = Box()
        box2.setPlainText('Box2')

        box3 = Box()
        box3.setPlainText('Box3')

        self.__scene.addItem(box1)
        self.__scene.addItem(box2)
        self.__scene.addItem(box3)
        view.setScene(self.__scene)

        self.setCentralWidget(view)