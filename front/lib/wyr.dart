import 'package:flutter/material.dart';

/// Flutter code sample for [Card].

class CardExampleApp extends StatelessWidget {
  const CardExampleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        //title: const Text('Would You Rather'),
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
          Text('Would You Rather ?', style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
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