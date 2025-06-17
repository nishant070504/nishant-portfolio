#ifdef BEYOND_THE_PLAYBOOK_H
#define BEYOND_THE_PLAYBOOK_H

#include <string>
#include <vector>


class PersonalityTrait{
private:
    std: string type;

public:
    PersonalityTrait(std: string type);
    void affectFocus();
    void affectMorale();
    std :: string gettype() const;


    
};

class FocusMeter{
private:
    int currentMeter;
    int maxFocus;

public:
    FocusMeter (int max);
    void increase(int amount);
    void decrease(int amount);
    int GetcurrentFocus()const;

};

class Player{
private:
    std::string name;
    std::string position;
    int rating;
    FocusMeter focus;
    Morale morale;
    std::vector<PersonalityTrait> traits;

public:
    Player(std::string name,std::string position,int rating);
    void train();
    void play();
    void reactToEvent(std::string eventType);
    void addTrait(const PersonalityTrait& trait);
    std::string getName() const;

};

class TeamEvent{
private:
    std::string eventType;
    int severity;

public:
    TeamEvent(std::string eventType,int severity);
    void affectPlayer(Player& player);
    void triggerDecision();

};

class DisciplinaryAction {
private:
    std::string actionType;

public:
    DisciplinaryAction(std::string type);
    void applyToPlayer(Player& player);
};

class Team {
private:
    std::vector<Player> players;
    int chemistry;
    int cultureLevel;

public:
    void addPlayer(const Player& player);
    void updateCulture();
    void evaluatePerformance();
    int getTeamSize() const;
};

class Coach {
private:
    std::string name;
    std::string disciplineStyle;
    std::vector<DisciplinaryAction> history;

public:
    Coach(std::string name, std::string style);
    void decideAction(Player& player, TeamEvent event);
    void handleEvent(TeamEvent event);
    void managePlayer(Player& player);
};

#endif;




