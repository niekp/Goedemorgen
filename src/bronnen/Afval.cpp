#include "Afval.h"

Afval::Afval() : Bron::Bron()
{
	// Dag van de week
	time_t t = time(NULL);
	tm* timePtr = localtime(&t);

	dagNu = timePtr->tm_wday;

	// Afval dagen
	afvalDag.insert(pair<int, string>(1, "plastic")); 
	afvalDag.insert(pair<int, string>(4, "papier")); 

	// Zoek afval voor vandaag op
	itVandaag = afvalDag.find(dagNu);
	if (itVandaag != afvalDag.end()) 
	{
		text = "Vandaag moet het " + itVandaag->second + " bij de weg.";
		hasText = true;
	}
}

bool Afval::HasText()
{
	return hasText;
}

string Afval::GetText()
{
	return text;
}