using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bullet : MonoBehaviour
{
	public GameObject hitEffect;
	
	void OnCollisionEnter2D(Collision2D collision)
	{
		
		GameObject effect = Instantiate(hitEffect, transform.position, Quaternion.identity);
		Destroy(gameObject);
		Destroy(effect, .15f);
	}
	
	void Update(){
		
    	if (!GetComponent<Renderer>().isVisible){
    		Destroy(gameObject);
		}
		
    }
}
