qid = QInputDialog()
canvas = iface.mapCanvas()
input, ok = QInputDialog.getText( qid, "Enter Coordinates", "Enter New Coordinates as 'xcoord,ycoord'", QLineEdit.Normal, "X" + "," + "Y")
if ok:
    x = input.split( "," )[ 0 ]
    print (x)
    y = input.split( "," )[ 1 ]
    print (y)
    if not x:
        print ("Ooops!X value is missing!")
    if not y:
        print ("Ooops!Y value is missing!")
    print (x + "," + y)
    scale=50
    rect = QgsRectangle(float(x)-scale,float(y)-scale,float(x)+scale,float(y)+scale)
    canvas.setExtent(rect)
    pt = QgsPoint(float(x),float(y))
    canvas.refresh()