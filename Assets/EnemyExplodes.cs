using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class enemyexplodes : MonoBehaviour
{

	public Rigidbody2D rb;
	public Transform target;

    // Start is called before the first frame update
    void Start()
    {
        rb = this.GetComponent<Rigidbody2D>();
        target = GameObject.FindGameObjectWithTag("Player 1").GetComponent<Transform>();
    }

   void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.tag == "Player 1")
        {
            Destroy(collision.gameObject);
        }
    }
}
