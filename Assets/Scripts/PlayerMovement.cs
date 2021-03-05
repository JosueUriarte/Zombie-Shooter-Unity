using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
	public float moveSpeed = 10f;
	public Rigidbody2D rb;
	public Camera cam;
	public GameObject player;
	
	Vector2 movement;
	Vector2 mousePos;
    // Start is called before the first frame update

    // Update is called once per frame
    void Update()
    {
		movement.x = Input.GetAxisRaw("Horizontal");
		movement.y = Input.GetAxisRaw("Vertical");
		
		mousePos = cam.ScreenToWorldPoint(Input.mousePosition);

		player = GameObject.FindGameObjectWithTag("Player");
    }
	
	/*void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.tag == "Enemy")
        {
            Destroy(collision.gameObject);
        }
    }*/

	void FixedUpdate() 
	{
		rb.MovePosition(rb.position + movement * moveSpeed * Time.fixedDeltaTime);
		
		Vector2 lookDir = mousePos - rb.position;
		
		float angle = Mathf.Atan2(lookDir.y, lookDir.x) * Mathf.Rad2Deg + 5f;
		
		rb.rotation = angle;
	}

}
