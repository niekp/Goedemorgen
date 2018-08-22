#pragma once
#include <string>
#include <map>
#include "Bron.h"

using namespace std;

class Weer : public Bron
{
	public:
		Weer();
		bool HasText();
		string GetText();

	private:
		string text;
		bool hasText;
};