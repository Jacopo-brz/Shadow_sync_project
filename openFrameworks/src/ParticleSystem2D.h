#pragma once
#include "ofMain.h"
#include "Particle2D.h"

class ParticleSystem2D
{
public:
	void setup(glm::vec2& shadowOrigin, int numParticles, int ParticleRadius, int particleLifespan);
	void update();
	void draw();
	void setOrigin(int x, int y);
	void moveOrigin(glm::vec2 & newOrigin);
	void setDestination(int x, int y);
	void moveDestination(int x_dir, int y_dir);
	void addParticle();
	void decay();
	void updateParticleMaxVals(float ms, float mf);
	void setAttractor(Circle* attractor);
	int origin_idx_in_shadow_junction_domain;
private:
	int numParticles, particleRadius, particleLifespan;
	glm::vec2 origin_PS2D;
	glm::vec2 destination;
	vector <Particle2D> particles;
	Circle* attractor; //pointer to junctions - attractors
};
