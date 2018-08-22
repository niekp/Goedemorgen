#include "Weer.h"

Weer::Weer() : Bron::Bron()
{
	// lat 52.992752
	// long 6.564228
	// https://api.darksky.net/forecast/01a688ebb1dc9a66788f4ec45cba4f48/52.992752,6.564228?units=auto
	// .daily > opzoek naar de timestamp op de juiste dag en dan temperatureMin en temperatureMax
	text = "";
	hasText = false;
}

bool Weer::HasText()
{
	return hasText;
}

string Weer::GetText()
{
	return text;
}