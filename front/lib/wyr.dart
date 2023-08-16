import 'package:flutter/material.dart';

/// Flutter code sample for [Card].

class CardExampleApp extends StatelessWidget {
  const CardExampleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          children: [
            const Padding(
              padding: EdgeInsets.only(top: 10),
              child: Text(
              "Would you rather ?",
              ),
            ),
            GestureDetector(
              child: const Text('sample subtitle', style: TextStyle(fontSize: 13)),
              onTap: () {
                
              },
            )
          ]
        ),
      ),
      body: const Center(
        child: CardExample()
      ),
    );
  }
}

class CardExample extends StatelessWidget {
  const CardExample({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          Choice(
            buttonText: "Installer NeoVim",
          ),
          SizedBox(height: 50),
          Text('OR', style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold)),
          SizedBox(height: 50),
          Choice(
            buttonText: "Installer Emacs",
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