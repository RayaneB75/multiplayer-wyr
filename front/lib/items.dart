
import 'package:flutter/material.dart';

class TextFieldCustom extends StatefulWidget {

    final String content;
    final TextEditingController controller;

    const TextFieldCustom({Key? key, required this.content, required this.controller}) : super(key: key);

  @override
  State<TextFieldCustom> createState() => _TextFieldCustomState();
}

class _TextFieldCustomState extends State<TextFieldCustom> {

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
          controller: widget.controller,
          decoration: InputDecoration(
            border: const OutlineInputBorder(),
            labelText: widget.content,
          ),
        ),
      );
  }
}