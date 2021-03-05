using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerHealth : MonoBehaviour
{
	
	public float maxHealth = 10f;
	public float currentHealth = 10f;
	
	void OnCollisionEnter2D(Collision2D collision)
    {	
        if (collision.gameObject.tag == "Enemy")
        {
			currentHealth = currentHealth - 1;
        }
    }
	
	void Update()
	{
		if (currentHealth == 0)
		{
			SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
		}
	}



}
