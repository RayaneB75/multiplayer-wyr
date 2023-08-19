import 'package:flutter/material.dart';

class WyrWindow extends StatelessWidget {

  final String firstProp;
  final String secondProp;
  
  const WyrWindow({super.key, required this.firstProp, required this.secondProp});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // appBar: AppBar(
      //   title: Column(
      //     mainAxisAlignment: MainAxisAlignment.center,
      //     crossAxisAlignment: CrossAxisAlignment.center,
      //     children: [
      //       const Padding(
      //         padding: EdgeInsets.only(top: 10),
      //         child: Text(
      //         "Would you rather ?",
      //         ),
      //       ),
      //       GestureDetector(
      //         child: const Text('sample subtitle', style: TextStyle(fontSize: 13)),
      //         onTap: () {
                
      //         },
      //       )
      //     ]
      //   ),
      // ),
      appBar: AppBar(
        title: Image.asset(
          'assets/logo_resel.png',
          fit: BoxFit.contain,
          height: 32,
          
        ),
      ),
      body: Center(
        child: Wyr(firstProp: firstProp, secondProp: secondProp)
      ),
    );
  }
}

class Wyr extends StatelessWidget {

  final String firstProp;
  final String secondProp;

  const Wyr({super.key, required this.firstProp, required this.secondProp});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          const Text('Tu préfères ?', style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold)),
          const SizedBox(height: 120),
          Choice(
            buttonText: firstProp,
          ),
          const SizedBox(height: 50),
          const Text('Ou', style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold)),
          const SizedBox(height: 50),
          Choice(
            buttonText: secondProp,
          ),
        ],
      ),
    );
  }
}

class Choice extends StatelessWidget {
  final String buttonText;

  const Choice({Key? key, required this.buttonText}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 300.0,
      height: 100.0,
      child: ElevatedButton(
        onPressed: () {},
        child: Text(
          buttonText,
          style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold)
        ),
      ),
    );
  }
}