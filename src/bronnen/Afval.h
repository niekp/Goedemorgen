#pragma once
#include <string>
#include <map>
#include "Bron.h"

using namespace std;

class Afval : public Bron
{
	public:
		Afval();
		bool HasText();
		string GetText();

	private:
		string text;
		bool hasText;
		int dagNu;
		map<int, string> afvalDag;
		map<int, string>::iterator itVandaag;
};