# pyqt-styled-graphics-text-item-example
Styled QGraphicsTextItem example

## Requirements
* PyQt5 >= 5.8

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-styled-graphics-text-item-example.git --upgrade```

## Example
Code Sample
```python
from PyQt5.QtWidgets import QApplication
from pyqt_styled_graphics_text_item_example import StyleGraphicsTextItemExample


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = StyleGraphicsTextItemExample()
    ex.show()
    sys.exit(app.exec_())
```

Result

![image](https://user-images.githubusercontent.com/55078043/152906777-bfad6e55-9c45-4f2f-857f-79f5f7ffab30.png)

Note: The position of each boxes have nothing to do with code. I moved them to show result well to you.
