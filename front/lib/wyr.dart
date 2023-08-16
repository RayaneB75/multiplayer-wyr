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
          Choice(),
          SizedBox(height: 50),
          Text('Would You Rather ?', style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
          SizedBox(height: 50),
          Choice(),
        ],
      ),
    );
  }
}

class Choice extends StatelessWidget {
    const Choice({super.key});

    @override
  Widget build(BuildContext context) {
    return Card(
        child: Column(
          children: <Widget>[
            const ListTile(
              //leading: Icon(Icons.album),
              title: Text('SAMPLE QUESTION'),
            subtitle: Text('sample description'),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                TextButton(
                  child: const Text('Sample Button'),
                  onPressed: () {/* ... */},
                ),
                const SizedBox(width: 8),
              ],
            ),
          ],
        ),
      );
  }


}