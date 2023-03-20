import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';

class ConnectWithCar extends StatefulWidget {
  final BluetoothDevice server;

  const ConnectWithCar({this.server});

  @override
  _ConnectWithCar createState() => new _ConnectWithCar();
}

class _Message {
  int whom;
  String text;

  _Message(this.whom, this.text);
}

class _ConnectWithCar extends State<ConnectWithCar> {
  static final clientID = 0;
  BluetoothConnection connection;
  String distance = "0";
  String orientation = 'N';
  String obstacle = "0";

  List<_Message> messages = List<_Message>();
  String _messageBuffer = '';

  final TextEditingController textEditingController =
      new TextEditingController();
  final ScrollController listScrollController = new ScrollController();

  bool isConnecting = true;
  bool get isConnected => connection != null && connection.isConnected;

  bool isDisconnecting = false;

  @override
  void initState() {
    super.initState();

    BluetoothConnection.toAddress(widget.server.address).then((_connection) {
      print('Connected to the device');
      connection = _connection;
      setState(() {
        isConnecting = false;
        isDisconnecting = false;
      });

      connection.input.listen(_onDataReceived).onDone(() {
        if (isDisconnecting) {
          print('Disconnecting locally!');
        } else {
          print('Disconnected remotely!');
        }
        if (this.mounted) {
          setState(() {});
        }
      });
    }).catchError((error) {
      print('Cannot connect, exception occured');
      print(error);
    });
  }

  @override
  void dispose() {
    // Avoid memory leak (`setState` after dispose) and disconnect
    if (isConnected) {
      isDisconnecting = true;
      connection.dispose();
      connection = null;
    }

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final List<Row> list = messages.map((_message) {
      return Row(
        children: <Widget>[
          Container(
            child: Text(
                (text) {
                  return text == '/shrug' ? '¯\\_(ツ)_/¯' : text;
                }(_message.text.trim()),
                style: TextStyle(color: Colors.white)),
            padding: EdgeInsets.all(12.0),
            margin: EdgeInsets.only(bottom: 8.0, left: 8.0, right: 8.0),
            width: 222.0,
            decoration: BoxDecoration(
                color:
                    _message.whom == clientID ? Colors.blueAccent : Colors.grey,
                borderRadius: BorderRadius.circular(7.0)),
          ),
        ],
        mainAxisAlignment: _message.whom == clientID
            ? MainAxisAlignment.end
            : MainAxisAlignment.start,
      );
    }).toList();

    Widget middleArrowSegment = Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        InkWell(
          onTap: () {
            debugPrint("\nLEFT\n");
            _sendMessage("LEFT");
          }, // Image tapped
          splashColor: Colors.white10, // Splash color over image
          child: Ink.image(
            fit: BoxFit.cover, // Fixes border issues
            width: 70,
            height: 70,
            image: AssetImage(
              'images/left-arrow.png',
            ),
          ),
        ),
        InkWell(
          onTap: () {
            debugPrint("\nRIGHT\n");
            _sendMessage("RIGHT");
          }, // Image tapped
          splashColor: Colors.white10, // Splash color over image
          child: Ink.image(
            fit: BoxFit.cover, // Fixes border issues
            width: 70,
            height: 70,
            image: AssetImage(
              'images/right-arrow.png',
            ),
          ),
        )
      ],
    );

    Widget upArrowSegment = Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        InkWell(
          onTap: () {
            debugPrint("\nUP\n");
            _sendMessage("UP");
          }, // Image tapped
          splashColor: Colors.white10, // Splash color over image
          child: Ink.image(
            fit: BoxFit.cover, // Fixes border issues
            width: 70,
            height: 70,
            image: AssetImage(
              'images/up-arrow.png',
            ),
          ),
        )
      ],
    );

    Widget downArrowSegment = Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        InkWell(
          onTap: () {
            debugPrint("\nDOWN\n");
            _sendMessage("DOWN");
          }, // Image tapped
          splashColor: Colors.white10, // Splash color over image
          child: Ink.image(
            fit: BoxFit.cover, // Fixes border issues
            width: 70,
            height: 70,
            image: AssetImage(
              'images/down-arrow.png',
            ),
          ),
        ),
      ],
    );

    return Scaffold(
      appBar: AppBar(
          title: (isConnecting
              ? Text('Connecting chat to ' + widget.server.name + '...')
              : isConnected
                  ? Text('Live chat with ' + widget.server.name)
                  : Text('Chat log with ' + widget.server.name))),
      body: SafeArea(
        child: Column(
          children: <Widget>[
          Column(
          mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              upArrowSegment,
              middleArrowSegment,
              downArrowSegment,
              Text('Distance: ' + distance + ' cm', style: TextStyle(fontSize: 25)),
              Text('Orientation: ' + orientation, style: TextStyle(fontSize: 25)),
              Text('Distance from obstacle: ' + obstacle + ' cm', style: TextStyle(fontSize: 25)),
            ],
          ),
            ],
        ),
      ),
    );
  }

  void _onDataReceived(Uint8List data) {
    // Allocate buffer for parsed data

    int backspacesCounter = 0;

    Uint8List buffer = Uint8List(data.length - backspacesCounter);

    // Create message if there is new line character
    String dataString = String.fromCharCodes(buffer);

    List<String> resultArr = dataString.split(",");

    setState(() {
      orientation = resultArr[0].substring(2,resultArr[0].length);
      distance = double.parse(resultArr[1]).toStringAsFixed(2);
      obstacle = double.parse(resultArr[2].substring(0, resultArr[2].length-2)).toStringAsFixed(2);
    });

  }

  void _sendMessage(String text) async {
    text = text.trim();
    textEditingController.clear();

    if (text.length > 0) {
      try {
        connection.output.add(utf8.encode(text));
        await connection.output.allSent;

        setState(() {
          messages.add(_Message(clientID, text));
        });

      } catch (e) {
        // Ignore error, but notify state
        setState(() {});
      }
    }
  }
}
