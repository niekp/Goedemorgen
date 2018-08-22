#include "Bron.h"

Bron::Bron()
{
	hasText = false;
	text = "";
}

bool Bron::HasText()
{
	return hasText;
}

string Bron::GetText()
{
	return text;
}
