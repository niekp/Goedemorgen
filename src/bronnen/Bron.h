#pragma once
#include <string>

using namespace std;

class Bron
{
	public:
		Bron();
		virtual bool HasText();
		virtual string GetText();

	private:
		string text;
		bool hasText;
};