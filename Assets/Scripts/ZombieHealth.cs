using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ZombieHealth : MonoBehaviour
{
	
	public float zmaxHealth = 8f;
	public float zcurrentHealth = 8f;
	
	void OnCollisionEnter2D(Collision2D collision)
    {	
        if (collision.gameObject.tag == "Bullet")
        {
			zcurrentHealth = zcurrentHealth - 1;
        }
		if (collision.gameObject.tag == "Explosion")
		{
			zcurrentHealth = zcurrentHealth + 0;
		}
    }
	
	void Update()
	{
		if (zcurrentHealth <= 0)
		{
			Destroy(gameObject);
		}
	}
	


}
