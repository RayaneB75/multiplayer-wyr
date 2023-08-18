
import 'package:flutter/material.dart';

class TextFieldCustom extends StatefulWidget {

    final String content;

    const TextFieldCustom({Key? key, required this.content}) : super(key: key);

  @override
  State<TextFieldCustom> createState() => _TextFieldCustomState();
}

class _TextFieldCustomState extends State<TextFieldCustom> {

  final myController = TextEditingController();

  @override
  void dispose() {
    // Clean up the controller when the widget is disposed.
    myController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
      return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 16),
        child: TextFormField(
          validator: (value) {
              if (value == null || value.isEmpty) {
                return 'S\'il vous plait renseignez ce champ';
              }
              return null;
            },
          controller: myController,
          decoration: InputDecoration(
            border: const OutlineInputBorder(),
            labelText: widget.content,
          ),
        ),
      );
  }
}