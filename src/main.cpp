#include <iostream>
#include <vector>

#include "bronnen/Bron.h"
#include "bronnen/Afval.h"

using namespace std;

int main() 
{
	// Vector van bronnen maken om alle bronnen aan toe te voegen.
	vector<Bron*> bronnen;

	// Voeg de gewenste bronnen toe
	bronnen.push_back(new Afval());

	// Bouw de tekst op
	for(auto const& bron: bronnen) {
		if (bron->HasText())
		{
			cout << bron->GetText();
			cout << endl;
		}
	}

	// Einde
	cout << endl;
	return 0;
}