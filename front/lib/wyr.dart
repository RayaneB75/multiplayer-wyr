import 'package:flutter/material.dart';

import 'api_calls.dart';

class WyrWindow extends StatelessWidget {
  final String firstProp;
  final String secondProp;
  final int userId;
  final String playedUser;

  const WyrWindow(
      {super.key,
      required this.firstProp,
      required this.secondProp,
      required this.userId,
      required this.playedUser});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        title: Image.asset(
          'assets/logo_resel.png',
          fit: BoxFit.contain,
          height: 32,
        ),
      ),
      body: Center(
          child: Wyr(
              firstProp: firstProp,
              secondProp: secondProp,
              userId: userId,
              playedUser: playedUser)),
    );
  }
}

class Wyr extends StatelessWidget {
  final String firstProp;
  final String secondProp;
  final int userId;
  final String playedUser;

  const Wyr(
      {super.key,
      required this.firstProp,
      required this.secondProp,
      required this.userId,
      required this.playedUser});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          Text('Tu joue actuellement avec : $playedUser',
              style:
                  const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 50),
          const Text('Tu préfères ?',
              style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold)),
          const SizedBox(height: 120),
          Choice(
            buttonText: firstProp,
            userId: userId,
          ),
          const SizedBox(height: 50),
          const Text('Ou',
              style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold)),
          const SizedBox(height: 50),
          Choice(
            buttonText: secondProp,
            userId: userId,
          ),
          const SizedBox(height: 150),
          ElevatedButton(
            child: const Text('Nouvelles propositions'),
            onPressed: () {
              ApiCalls.pullQuestions(context, playedUser); // stateless solution
            },
          ),
        ],
      ),
    );
  }
}

class Choice extends StatelessWidget {
  final String buttonText;
  final int userId;

  const Choice({Key? key, required this.buttonText, required this.userId})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 300.0,
      height: 100.0,
      child: ElevatedButton(
        onPressed: () {
          ApiCalls.pushAnswer(context);
        },
        child: Text(
            textAlign: TextAlign.center,
            buttonText,
            style: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.bold,
            )),
      ),
    );
  }
}
