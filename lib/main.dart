import 'dart:io';

import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Senman',
      theme: ThemeData(
        primarySwatch: Colors.indigo,
      ),
      home: MyHomePage(title: 'Senman'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  
  double iniX;
  double endX;
  double iniY;
  double endY;

  double iniScroll;

  Socket socket;

  @override
  void initState() {
    super.initState();

    Socket.connect('192.168.15.87', 1987).then((io) {
      this.socket = io;
      print(this.socket);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        actions: <Widget>[
          IconButton(
            icon: Icon(Icons.close),
            onPressed: () {
              this.socket.close();
            },
          )
        ],
      ),
      body: Column(
        children: <Widget>[
          Expanded(child: Container(
              color: Colors.grey,
              child: Center(child: GestureDetector(
                child: Container(
                  color: Colors.white,
                  width: MediaQuery.of(context).size.width-20,
                  height: (9*(MediaQuery.of(context).size.width-20))/16,
                ),
                onPanStart: (details) {
                  this.iniX = details.localPosition.dx;
                  this.iniY = details.localPosition.dy;
                },
                onPanUpdate: (details) {

                  this.endX = details.localPosition.dx;
                  this.endY = details.localPosition.dy;
                  
                  int theX = (this.sensitivity((this.iniX - this.endX)*-1)).round();
                  int theY = (this.sensitivity(this.iniY - this.endY)).round();

                  if (theX == 0 && theY == 0) {
                    return;
                  }

                  String mouseX = 'mouseX=';
                  mouseX += (!theX.isNegative) ? '+' : '';
                  mouseX += theX.toString();

                  String mouseY = 'mouseY=';
                  mouseY += (!theY.isNegative) ? '+' : '';
                  mouseY += theY.toString();

                  this.socket.write(mouseX+'&'+mouseY+';');
                },
                // onTap: () {
                //   this.socket.write('leftclick;');
                // },
                // onDoubleTap: () {
                //   this.socket.write('doubleclick;');
                // },
                // onLongPress: () {
                //   this.socket.write('rightclick;');
                // },
              ),
            ),
          )),
          Container(
            height: 100,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                GestureDetector(
                  child: Container(
                    color: Colors.black54,
                    width: (MediaQuery.of(context).size.width/12)*5,
                  ),
                  onTap: () {
                    this.socket.write('leftclick;');
                  },
                  onDoubleTap: () {
                    this.socket.write('doubleclick;');
                  },
                ),
                SizedBox(width: 0.3),
                Expanded(child: GestureDetector(
                  child: Container(
                    color: Colors.black45,
                  ),
                  onPanStart: (details) {
                    this.iniScroll = details.localPosition.dy;
                  },
                  onPanUpdate: (details) {

                    int scroll = (this.iniScroll - details.localPosition.dy).round();
                    scroll = scroll~/8; // Divide e transforma em int novamente

                    if (scroll == 0) {
                      return;
                    }

                    if (scroll.isNegative) {
                      this.socket.write('scroll='+scroll.toString()+';');
                    } else {
                      this.socket.write('scroll=+'+scroll.toString()+';');
                    }

                  },
                )),
                SizedBox(width: 0.3),
                GestureDetector(
                  child: Container(
                    color: Colors.black54,
                    width: (MediaQuery.of(context).size.width/12)*5,
                  ),
                  onTap: () {
                    this.socket.write('rightclick;');
                  },
                ),
              ],
            ),
          )
        ],
      ),
    );
  }

  double sensitivity(double value, [double sensitivity = 100])
  {
    return (value/100)*sensitivity;
  }
}
