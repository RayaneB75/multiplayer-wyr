
import 'package:flutter/material.dart';

class TextFieldCustom extends StatelessWidget {

    final String content;

    const TextFieldCustom({Key? key, required this.content}) : super(key: key);

    @override
    Widget build(BuildContext context) {
        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 16),
          child: TextFormField(
            decoration: InputDecoration(
              border: const OutlineInputBorder(),
              labelText: content,
            ),
          ),
        );
    }
}